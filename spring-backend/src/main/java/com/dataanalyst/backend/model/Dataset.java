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
public class Dataset {
    private String id;
    private String userId;
    private String fileName;
    private String storagePath;
    private String storageUrl;
    private long fileSizeBytes;
    private String fileType; // CSV, XLSX, etc.
    private Instant uploadedAt;
    private boolean processed;
    private int rowCount;
    private int columnCount;
}
