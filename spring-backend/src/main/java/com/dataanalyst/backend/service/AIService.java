package com.dataanalyst.backend.service;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;

import java.util.HashMap;
import java.util.Map;

@Service
public class AIService {

    private static final Logger logger = LoggerFactory.getLogger(AIService.class);
    private final WebClient pythonServiceWebClient;

    public AIService(WebClient pythonServiceWebClient) {
        this.pythonServiceWebClient = pythonServiceWebClient;
    }

    public Map<String, Object> processDataset(String datasetId, String fileUrl, String fileName) {
        logger.info("Sending dataset to Python service for processing: {}", datasetId);

        Map<String, Object> request = new HashMap<>();
        request.put("datasetId", datasetId);
        request.put("fileUrl", fileUrl);
        request.put("fileName", fileName);

        try {
            @SuppressWarnings("unchecked")
            Map<String, Object> response = (Map<String, Object>) pythonServiceWebClient.post()
                    .uri("/api/process")
                    .bodyValue(request)
                    .retrieve()
                    .bodyToMono(Map.class)
                    .block();

            logger.info("Dataset processing response received: {}", response);
            return response;
        } catch (Exception e) {
            logger.error("Error processing dataset: {}", e.getMessage(), e);
            Map<String, Object> errorResponse = new HashMap<>();
            errorResponse.put("success", false);
            errorResponse.put("error", e.getMessage());
            return errorResponse;
        }
    }

    public Map<String, Object> queryDataset(String datasetId, String query, String userId) {
        logger.info("Sending query to Python service for dataset: {}", datasetId);

        Map<String, Object> request = new HashMap<>();
        request.put("datasetId", datasetId);
        request.put("query", query);
        request.put("userId", userId);

        try {
            @SuppressWarnings("unchecked")
            Map<String, Object> response = (Map<String, Object>) pythonServiceWebClient.post()
                    .uri("/api/query")
                    .bodyValue(request)
                    .retrieve()
                    .bodyToMono(Map.class)
                    .block();

            logger.info("Query response received");
            return response;
        } catch (Exception e) {
            logger.error("Error querying dataset: {}", e.getMessage(), e);
            Map<String, Object> errorResponse = new HashMap<>();
            errorResponse.put("success", false);
            errorResponse.put("error", e.getMessage());
            return errorResponse;
        }
    }

    public boolean checkPythonServiceHealth() {
        logger.info("Checking Python service health");

        try {
            pythonServiceWebClient.get()
                    .uri("/health")
                    .retrieve()
                    .bodyToMono(String.class)
                    .block();

            logger.info("Python service health check successful");
            return true;
        } catch (Exception e) {
            logger.error("Python service health check failed: {}", e.getMessage());
            return false;
        }
    }
}
