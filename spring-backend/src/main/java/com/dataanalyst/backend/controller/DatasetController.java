package com.dataanalyst.backend.controller;

import com.dataanalyst.backend.dto.UploadResponse;
import com.dataanalyst.backend.model.Dataset;
import com.dataanalyst.backend.service.AIService;
import com.dataanalyst.backend.service.FirebaseService;
import com.dataanalyst.backend.service.StorageService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.time.Instant;
import java.util.List;
import java.util.Map;
import java.util.UUID;

@RestController
@RequestMapping("/api/datasets")
public class DatasetController {

    private static final Logger logger = LoggerFactory.getLogger(DatasetController.class);

    private final FirebaseService firebaseService;
    private final StorageService storageService;
    private final AIService aiService;

    public DatasetController(FirebaseService firebaseService,
            StorageService storageService,
            AIService aiService) {
        this.firebaseService = firebaseService;
        this.storageService = storageService;
        this.aiService = aiService;
    }

    @PostMapping("/upload")
    public ResponseEntity<UploadResponse> uploadDataset(
            @RequestParam("file") MultipartFile file,
            @RequestParam("userId") String userId) {

        try {
            logger.info("Upload request from user: {} for file: {}", userId, file.getOriginalFilename());

            // Validate file
            if (file.isEmpty()) {
                return ResponseEntity.badRequest().body(
                        UploadResponse.builder()
                                .success(false)
                                .message("File is empty")
                                .build());
            }

            // Validate file type
            String contentType = file.getContentType();
            if (!isValidFileType(contentType)) {
                return ResponseEntity.badRequest().body(
                        UploadResponse.builder()
                                .success(false)
                                .message("Invalid file type. Only CSV and Excel files are supported.")
                                .build());
            }

            // Upload to Firebase Storage
            String storagePath = storageService.uploadFile(file, userId);
            String storageUrl = storageService.getSignedUrl(storagePath);

            // Create dataset metadata
            String datasetId = UUID.randomUUID().toString();
            Dataset dataset = Dataset.builder()
                    .id(datasetId)
                    .userId(userId)
                    .fileName(file.getOriginalFilename())
                    .storagePath(storagePath)
                    .storageUrl(storageUrl)
                    .fileSizeBytes(file.getSize())
                    .fileType(getFileExtension(file.getOriginalFilename()))
                    .uploadedAt(Instant.now())
                    .processed(false)
                    .rowCount(0)
                    .columnCount(0)
                    .build();

            // Save to Firestore
            firebaseService.createDataset(dataset);

            // Send to Python service for processing (async)
            new Thread(() -> {
                try {
                    logger.info("Sending dataset to Python service for processing: {}", datasetId);
                    Map<String, Object> processResult = aiService.processDataset(
                            datasetId,
                            storageUrl,
                            file.getOriginalFilename());

                    // Update dataset with processing results
                    if (processResult != null && (Boolean) processResult.get("success")) {
                        int rowCount = (Integer) processResult.getOrDefault("rowCount", 0);
                        int columnCount = (Integer) processResult.getOrDefault("columnCount", 0);

                        firebaseService.updateDatasetProcessingStatus(datasetId, true, rowCount, columnCount);
                        logger.info("Dataset processed successfully: {}", datasetId);
                    } else {
                        logger.error("Dataset processing failed: {}", processResult);
                    }
                } catch (Exception e) {
                    logger.error("Error processing dataset: {}", e.getMessage(), e);
                }
            }).start();

            UploadResponse response = UploadResponse.builder()
                    .success(true)
                    .message("File uploaded successfully")
                    .datasetId(datasetId)
                    .fileName(file.getOriginalFilename())
                    .fileSizeBytes(file.getSize())
                    .storagePath(storagePath)
                    .build();

            return ResponseEntity.ok(response);

        } catch (Exception e) {
            logger.error("Error uploading file: {}", e.getMessage(), e);

            UploadResponse response = UploadResponse.builder()
                    .success(false)
                    .message("Upload failed: " + e.getMessage())
                    .build();

            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(response);
        }
    }

    @GetMapping
    public ResponseEntity<List<Dataset>> getUserDatasets(@RequestParam String userId) {
        try {
            logger.info("Fetching datasets for user: {}", userId);

            List<Dataset> datasets = firebaseService.getUserDatasets(userId);
            return ResponseEntity.ok(datasets);

        } catch (Exception e) {
            logger.error("Error fetching datasets: {}", e.getMessage(), e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }

    @GetMapping("/{id}")
    public ResponseEntity<Dataset> getDataset(@PathVariable String id) {
        try {
            logger.info("Fetching dataset: {}", id);

            Dataset dataset = firebaseService.getDataset(id);

            if (dataset == null) {
                return ResponseEntity.notFound().build();
            }

            return ResponseEntity.ok(dataset);

        } catch (Exception e) {
            logger.error("Error fetching dataset: {}", e.getMessage(), e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Map<String, Object>> deleteDataset(@PathVariable String id) {
        try {
            logger.info("Deleting dataset: {}", id);

            // Get dataset to find storage path
            Dataset dataset = firebaseService.getDataset(id);

            if (dataset == null) {
                return ResponseEntity.notFound().build();
            }

            // Delete from storage
            storageService.deleteFile(dataset.getStoragePath());

            // Delete from Firestore
            firebaseService.deleteDataset(id);

            return ResponseEntity.ok(Map.of(
                    "success", true,
                    "message", "Dataset deleted successfully"));

        } catch (Exception e) {
            logger.error("Error deleting dataset: {}", e.getMessage(), e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(Map.of(
                    "success", false,
                    "message", "Delete failed: " + e.getMessage()));
        }
    }

    private boolean isValidFileType(String contentType) {
        return contentType != null && (contentType.equals("text/csv") ||
                contentType.equals("application/vnd.ms-excel") ||
                contentType.equals("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"));
    }

    private String getFileExtension(String fileName) {
        int dotIndex = fileName.lastIndexOf('.');
        if (dotIndex > 0) {
            return fileName.substring(dotIndex + 1).toUpperCase();
        }
        return "UNKNOWN";
    }
}
