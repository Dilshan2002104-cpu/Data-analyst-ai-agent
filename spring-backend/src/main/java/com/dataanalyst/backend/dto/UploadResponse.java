package com.dataanalyst.backend.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class UploadResponse {
    private boolean success;
    private String message;
    private String datasetId;
    private String fileName;
    private long fileSizeBytes;
    private String storagePath;
}
