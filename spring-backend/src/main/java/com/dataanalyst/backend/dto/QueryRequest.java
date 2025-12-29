package com.dataanalyst.backend.dto;

import jakarta.validation.constraints.NotBlank;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class QueryRequest {
    @NotBlank(message = "Dataset ID is required")
    private String datasetId;

    @NotBlank(message = "Query is required")
    private String query;

    private String userId;
}
