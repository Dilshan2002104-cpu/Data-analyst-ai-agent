package com.dataanalyst.backend.controller;

import com.dataanalyst.backend.model.ChatMessage;
import com.dataanalyst.backend.service.FirebaseService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/chat")
@CrossOrigin(origins = "http://localhost:5173")
public class ChatController {

    private final FirebaseService firebaseService;

    public ChatController(FirebaseService firebaseService) {
        this.firebaseService = firebaseService;
    }

    @PostMapping
    public ResponseEntity<ChatMessage> saveMessage(@RequestBody ChatMessage message) {
        try {
            if (message.getId() == null || message.getId().isEmpty()) {
                message.setId("msg_" + java.util.UUID.randomUUID().toString());
            }

            ChatMessage saved = firebaseService.saveChatMessage(message);
            return ResponseEntity.ok(saved);
        } catch (Exception e) {
            return ResponseEntity.internalServerError().build();
        }
    }

    @GetMapping("/{datasetId}")
    public ResponseEntity<List<ChatMessage>> getChatHistory(@PathVariable String datasetId) {
        try {
            List<ChatMessage> messages = firebaseService.getChatHistory(datasetId);
            return ResponseEntity.ok(messages);
        } catch (Exception e) {
            return ResponseEntity.internalServerError().build();
        }
    }
}
