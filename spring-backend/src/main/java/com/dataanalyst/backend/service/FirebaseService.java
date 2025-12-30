package com.dataanalyst.backend.service;

import com.dataanalyst.backend.model.ChatMessage;
import com.dataanalyst.backend.model.Dataset;
import com.dataanalyst.backend.model.SQLConnection;
import com.dataanalyst.backend.model.User;
import com.google.cloud.firestore.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import java.time.Instant;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ExecutionException;

@Service
@SuppressWarnings("null")
public class FirebaseService {

    private static final Logger logger = LoggerFactory.getLogger(FirebaseService.class);
    private final Firestore firestore;

    private static final String USERS_COLLECTION = "users";
    private static final String DATASETS_COLLECTION = "datasets";
    private static final String CHAT_MESSAGES_COLLECTION = "chatMessages";
    private static final String SQL_CONNECTIONS_COLLECTION = "sqlConnections";

    public FirebaseService(Firestore firestore) {
        this.firestore = firestore;
    }

    // ============ User Operations ============

    public User createUser(User user) throws ExecutionException, InterruptedException {
        logger.info("Creating user: {}", user.getEmail());

        Map<String, Object> userData = new HashMap<>();
        userData.put("uid", user.getUid());
        userData.put("email", user.getEmail());
        userData.put("displayName", user.getDisplayName());
        userData.put("createdAt", user.getCreatedAt().toString());
        userData.put("lastLoginAt", user.getLastLoginAt().toString());

        firestore.collection(USERS_COLLECTION)
                .document(user.getUid())
                .set(userData)
                .get();

        logger.info("User created successfully: {}", user.getUid());
        return user;
    }

    public User getUser(String uid) throws ExecutionException, InterruptedException {
        logger.info("Fetching user: {}", uid);

        DocumentSnapshot document = firestore.collection(USERS_COLLECTION)
                .document(uid)
                .get()
                .get();

        if (!document.exists()) {
            logger.warn("User not found: {}", uid);
            return null;
        }

        return documentToUser(document);
    }

    public void updateLastLogin(String uid) throws ExecutionException, InterruptedException {
        logger.info("Updating last login for user: {}", uid);

        Map<String, Object> updates = new HashMap<>();
        updates.put("lastLoginAt", Instant.now().toString());

        firestore.collection(USERS_COLLECTION)
                .document(uid)
                .update(updates)
                .get();
    }

    // ============ Dataset Operations ============

    public Dataset createDataset(Dataset dataset) throws ExecutionException, InterruptedException {
        logger.info("Creating dataset: {} for user: {}", dataset.getFileName(), dataset.getUserId());

        Map<String, Object> datasetData = new HashMap<>();
        datasetData.put("id", dataset.getId());
        datasetData.put("userId", dataset.getUserId());
        datasetData.put("fileName", dataset.getFileName());
        datasetData.put("storagePath", dataset.getStoragePath());
        datasetData.put("storageUrl", dataset.getStorageUrl());
        datasetData.put("fileSizeBytes", dataset.getFileSizeBytes());
        datasetData.put("fileType", dataset.getFileType());
        datasetData.put("uploadedAt", dataset.getUploadedAt().toString());
        datasetData.put("processed", dataset.isProcessed());
        datasetData.put("rowCount", dataset.getRowCount());
        datasetData.put("columnCount", dataset.getColumnCount());

        firestore.collection(DATASETS_COLLECTION)
                .document(dataset.getId())
                .set(datasetData)
                .get();

        logger.info("Dataset created successfully: {}", dataset.getId());
        return dataset;
    }

    public Dataset getDataset(String datasetId) throws ExecutionException, InterruptedException {
        logger.info("Fetching dataset: {}", datasetId);

        DocumentSnapshot document = firestore.collection(DATASETS_COLLECTION)
                .document(datasetId)
                .get()
                .get();

        if (!document.exists()) {
            logger.warn("Dataset not found: {}", datasetId);
            return null;
        }

        return documentToDataset(document);
    }

    public List<Dataset> getUserDatasets(String userId) throws ExecutionException, InterruptedException {
        logger.info("Fetching datasets for user: {}", userId);

        QuerySnapshot querySnapshot = firestore.collection(DATASETS_COLLECTION)
                .whereEqualTo("userId", userId)
                .get()
                .get();

        List<Dataset> datasets = new ArrayList<>();
        for (DocumentSnapshot document : querySnapshot.getDocuments()) {
            datasets.add(documentToDataset(document));
        }

        // Sort in memory to avoid Firestore index requirement
        datasets.sort((d1, d2) -> d2.getUploadedAt().compareTo(d1.getUploadedAt()));

        logger.info("Found {} datasets for user: {}", datasets.size(), userId);
        return datasets;
    }

    public void updateDatasetProcessingStatus(String datasetId, boolean processed, int rowCount, int columnCount)
            throws ExecutionException, InterruptedException {
        logger.info("Updating processing status for dataset: {}", datasetId);

        Map<String, Object> updates = new HashMap<>();
        updates.put("processed", processed);
        updates.put("rowCount", rowCount);
        updates.put("columnCount", columnCount);

        firestore.collection(DATASETS_COLLECTION)
                .document(datasetId)
                .update(updates)
                .get();
    }

    public void deleteDataset(String datasetId) throws ExecutionException, InterruptedException {
        logger.info("Deleting dataset: {}", datasetId);

        firestore.collection(DATASETS_COLLECTION)
                .document(datasetId)
                .delete()
                .get();

        logger.info("Dataset deleted successfully: {}", datasetId);
    }

    // ============ SQL Connection Operations ============

    public SQLConnection saveConnection(SQLConnection connection) throws ExecutionException, InterruptedException {
        logger.info("Saving SQL connection: {}", connection.getName());

        Map<String, Object> connData = new HashMap<>();
        connData.put("id", connection.getId());
        connData.put("userId", connection.getUserId());
        connData.put("name", connection.getName());
        connData.put("type", connection.getType());
        connData.put("host", connection.getHost());
        connData.put("port", connection.getPort());
        connData.put("database", connection.getDatabase());
        connData.put("username", connection.getUsername());
        connData.put("password", connection.getPassword());
        connData.put("createdAt", connection.getCreatedAt());

        firestore.collection(SQL_CONNECTIONS_COLLECTION)
                .document(connection.getId())
                .set(connData)
                .get();

        logger.info("SQL connection saved successfully: {}", connection.getId());
        return connection;
    }

    public List<SQLConnection> getUserConnections(String userId) throws ExecutionException, InterruptedException {
        logger.info("Fetching SQL connections for user: {}", userId);

        QuerySnapshot querySnapshot = firestore.collection(SQL_CONNECTIONS_COLLECTION)
                .whereEqualTo("userId", userId)
                .get()
                .get();

        List<SQLConnection> connections = new ArrayList<>();
        for (DocumentSnapshot document : querySnapshot.getDocuments()) {
            connections.add(documentToSQLConnection(document));
        }

        logger.info("Found {} connections for user: {}", connections.size(), userId);
        return connections;
    }

    public void deleteConnection(String connectionId) throws ExecutionException, InterruptedException {
        logger.info("Deleting SQL connection: {}", connectionId);

        firestore.collection(SQL_CONNECTIONS_COLLECTION)
                .document(connectionId)
                .delete()
                .get();

        logger.info("Connection deleted: {}", connectionId);
    }

    // ============ Chat Message Operations ============

    public ChatMessage saveChatMessage(ChatMessage message) throws ExecutionException, InterruptedException {
        logger.info("Saving chat message for dataset: {}", message.getDatasetId());

        Map<String, Object> messageData = new HashMap<>();
        messageData.put("id", message.getId());
        messageData.put("datasetId", message.getDatasetId());
        messageData.put("userId", message.getUserId());
        messageData.put("userMessage", message.getUserMessage());
        messageData.put("aiResponse", message.getAiResponse());
        messageData.put("timestamp", message.getTimestamp().toString());
        messageData.put("responseTimeMs", message.getResponseTimeMs());

        firestore.collection(CHAT_MESSAGES_COLLECTION)
                .document(message.getId())
                .set(messageData)
                .get();

        logger.info("Chat message saved successfully: {}", message.getId());
        return message;
    }

    public List<ChatMessage> getChatHistory(String datasetId) throws ExecutionException, InterruptedException {
        logger.info("Fetching chat history for dataset: {}", datasetId);

        QuerySnapshot querySnapshot = firestore.collection(CHAT_MESSAGES_COLLECTION)
                .whereEqualTo("datasetId", datasetId)
                .get()
                .get();

        List<ChatMessage> messages = new ArrayList<>();
        for (DocumentSnapshot document : querySnapshot.getDocuments()) {
            messages.add(documentToChatMessage(document));
        }

        // Sort in memory to avoid Firestore index requirement
        messages.sort((m1, m2) -> m1.getTimestamp().compareTo(m2.getTimestamp()));

        logger.info("Found {} messages for dataset: {}", messages.size(), datasetId);
        return messages;
    }

    // ============ Helper Methods ============

    private User documentToUser(DocumentSnapshot document) {
        return User.builder()
                .uid(document.getString("uid"))
                .email(document.getString("email"))
                .displayName(document.getString("displayName"))
                .createdAt(Instant.parse(document.getString("createdAt")))
                .lastLoginAt(Instant.parse(document.getString("lastLoginAt")))
                .build();
    }

    private Dataset documentToDataset(DocumentSnapshot document) {
        Long fileSizeBytes = document.getLong("fileSizeBytes");
        Long rowCount = document.getLong("rowCount");
        Long columnCount = document.getLong("columnCount");
        Boolean processed = document.getBoolean("processed");

        return Dataset.builder()
                .id(document.getString("id"))
                .userId(document.getString("userId"))
                .fileName(document.getString("fileName"))
                .storagePath(document.getString("storagePath"))
                .storageUrl(document.getString("storageUrl"))
                .fileSizeBytes(fileSizeBytes != null ? fileSizeBytes : 0L)
                .fileType(document.getString("fileType"))
                .uploadedAt(Instant.parse(document.getString("uploadedAt")))
                .processed(processed != null ? processed : false)
                .rowCount(rowCount != null ? rowCount.intValue() : 0)
                .columnCount(columnCount != null ? columnCount.intValue() : 0)
                .build();
    }

    private ChatMessage documentToChatMessage(DocumentSnapshot document) {
        Long responseTimeMs = document.getLong("responseTimeMs");

        return ChatMessage.builder()
                .id(document.getString("id"))
                .datasetId(document.getString("datasetId"))
                .userId(document.getString("userId"))
                .userMessage(document.getString("userMessage"))
                .aiResponse(document.getString("aiResponse"))
                .timestamp(Instant.parse(document.getString("timestamp")))
                .responseTimeMs(responseTimeMs != null ? responseTimeMs : 0L)
                .build();
    }

    private SQLConnection documentToSQLConnection(DocumentSnapshot document) {
        Long port = document.getLong("port");

        return SQLConnection.builder()
                .id(document.getString("id"))
                .userId(document.getString("userId"))
                .name(document.getString("name"))
                .type(document.getString("type"))
                .host(document.getString("host"))
                .port(port != null ? port.intValue() : 3306)
                .database(document.getString("database"))
                .username(document.getString("username"))
                .password(document.getString("password"))
                .createdAt(document.getString("createdAt"))
                .build();
    }
}
