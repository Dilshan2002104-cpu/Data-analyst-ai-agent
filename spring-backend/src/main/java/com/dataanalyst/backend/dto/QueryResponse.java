package com.dataanalyst.backend.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class QueryResponse {
    private boolean success;
    private String response;
    private String error;
    private long responseTimeMs;
    private String messageId;
}
