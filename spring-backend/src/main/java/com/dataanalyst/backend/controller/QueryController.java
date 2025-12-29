package com.dataanalyst.backend.controller;

import com.dataanalyst.backend.dto.QueryRequest;
import com.dataanalyst.backend.dto.QueryResponse;
import com.dataanalyst.backend.model.ChatMessage;
import com.dataanalyst.backend.service.AIService;
import com.dataanalyst.backend.service.FirebaseService;
import jakarta.validation.Valid;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.time.Instant;
import java.util.List;
import java.util.Map;
import java.util.UUID;

@RestController
@RequestMapping("/api/query")
public class QueryController {

    private static final Logger logger = LoggerFactory.getLogger(QueryController.class);

    private final AIService aiService;
    private final FirebaseService firebaseService;

    public QueryController(AIService aiService, FirebaseService firebaseService) {
        this.aiService = aiService;
        this.firebaseService = firebaseService;
    }

    @PostMapping
    public ResponseEntity<QueryResponse> query(@Valid @RequestBody QueryRequest request) {
        long startTime = System.currentTimeMillis();

        try {
            logger.info("Query request for dataset: {} from user: {}",
                    request.getDatasetId(), request.getUserId());

            // Send query to Python AI service
            Map<String, Object> aiResponse = aiService.queryDataset(
                    request.getDatasetId(),
                    request.getQuery(),
                    request.getUserId());

            long responseTime = System.currentTimeMillis() - startTime;

            // Extract response
            boolean success = (Boolean) aiResponse.getOrDefault("success", false);
            String responseText = (String) aiResponse.get("response");
            String error = (String) aiResponse.get("error");

            if (success && responseText != null) {
                // Save to chat history
                String messageId = UUID.randomUUID().toString();
                ChatMessage message = ChatMessage.builder()
                        .id(messageId)
                        .datasetId(request.getDatasetId())
                        .userId(request.getUserId())
                        .userMessage(request.getQuery())
                        .aiResponse(responseText)
                        .timestamp(Instant.now())
                        .responseTimeMs(responseTime)
                        .build();

                firebaseService.saveChatMessage(message);

                QueryResponse response = QueryResponse.builder()
                        .success(true)
                        .response(responseText)
                        .responseTimeMs(responseTime)
                        .messageId(messageId)
                        .build();

                return ResponseEntity.ok(response);
            } else {
                QueryResponse response = QueryResponse.builder()
                        .success(false)
                        .error(error != null ? error : "Query failed")
                        .responseTimeMs(responseTime)
                        .build();

                return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(response);
            }

        } catch (Exception e) {
            logger.error("Error processing query: {}", e.getMessage(), e);

            long responseTime = System.currentTimeMillis() - startTime;

            QueryResponse response = QueryResponse.builder()
                    .success(false)
                    .error("Query failed: " + e.getMessage())
                    .responseTimeMs(responseTime)
                    .build();

            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(response);
        }
    }

    @GetMapping("/history/{datasetId}")
    public ResponseEntity<List<ChatMessage>> getChatHistory(@PathVariable String datasetId) {
        try {
            logger.info("Fetching chat history for dataset: {}", datasetId);

            List<ChatMessage> history = firebaseService.getChatHistory(datasetId);
            return ResponseEntity.ok(history);

        } catch (Exception e) {
            logger.error("Error fetching chat history: {}", e.getMessage(), e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }

    @GetMapping("/health")
    public ResponseEntity<Map<String, Object>> healthCheck() {
        boolean pythonServiceHealthy = aiService.checkPythonServiceHealth();

        return ResponseEntity.ok(Map.of(
                "status", "UP",
                "pythonService", pythonServiceHealthy ? "UP" : "DOWN",
                "timestamp", Instant.now().toString()));
    }
}
