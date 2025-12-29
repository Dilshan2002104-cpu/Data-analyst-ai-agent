package com.dataanalyst.backend.service;

import com.google.cloud.storage.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.UUID;
import java.util.concurrent.TimeUnit;

@Service
public class StorageService {

    private static final Logger logger = LoggerFactory.getLogger(StorageService.class);
    private final Storage storage;

    @Value("${firebase.storage-bucket}")
    private String bucketName;

    public StorageService(Storage storage) {
        this.storage = storage;
    }

    public String uploadFile(MultipartFile file, String userId) throws IOException {
        logger.info("Uploading file: {} for user: {}", file.getOriginalFilename(), userId);

        String fileName = generateFileName(file.getOriginalFilename(), userId);
        String contentType = file.getContentType();

        BlobId blobId = BlobId.of(bucketName, fileName);
        BlobInfo blobInfo = BlobInfo.newBuilder(blobId)
                .setContentType(contentType)
                .build();

        storage.create(blobInfo, file.getBytes());

        logger.info("File uploaded successfully: {}", fileName);
        return fileName;
    }

    public String getSignedUrl(String fileName) {
        logger.info("Generating signed URL for file: {}", fileName);

        BlobId blobId = BlobId.of(bucketName, fileName);
        Blob blob = storage.get(blobId);

        if (blob == null) {
            logger.error("File not found: {}", fileName);
            throw new RuntimeException("File not found: " + fileName);
        }

        // Generate signed URL valid for 7 days
        String signedUrl = blob.signUrl(7, TimeUnit.DAYS).toString();

        logger.info("Signed URL generated successfully");
        return signedUrl;
    }

    public String getPublicUrl(String fileName) {
        return String.format("https://storage.googleapis.com/%s/%s", bucketName, fileName);
    }

    public void deleteFile(String fileName) {
        logger.info("Deleting file: {}", fileName);

        BlobId blobId = BlobId.of(bucketName, fileName);
        boolean deleted = storage.delete(blobId);

        if (deleted) {
            logger.info("File deleted successfully: {}", fileName);
        } else {
            logger.warn("File not found or already deleted: {}", fileName);
        }
    }

    public byte[] downloadFile(String fileName) {
        logger.info("Downloading file: {}", fileName);

        BlobId blobId = BlobId.of(bucketName, fileName);
        Blob blob = storage.get(blobId);

        if (blob == null) {
            logger.error("File not found: {}", fileName);
            throw new RuntimeException("File not found: " + fileName);
        }

        return blob.getContent();
    }

    private String generateFileName(String originalFilename, String userId) {
        String extension = "";
        int dotIndex = originalFilename.lastIndexOf('.');
        if (dotIndex > 0) {
            extension = originalFilename.substring(dotIndex);
        }

        String timestamp = String.valueOf(System.currentTimeMillis());
        String uuid = UUID.randomUUID().toString().substring(0, 8);

        return String.format("datasets/%s/%s_%s%s", userId, timestamp, uuid, extension);
    }

    public long getFileSize(String fileName) {
        BlobId blobId = BlobId.of(bucketName, fileName);
        Blob blob = storage.get(blobId);

        if (blob == null) {
            return 0;
        }

        return blob.getSize();
    }
}
