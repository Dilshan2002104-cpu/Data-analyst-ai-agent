package com.dataanalyst.backend.model;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.Instant;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ChatMessage {
    private String id;
    private String datasetId;
    private String userId;
    private String userMessage;
    private String aiResponse;
    private Instant timestamp;
    private long responseTimeMs;
}
