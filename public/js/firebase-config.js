// firebase-config.js

import { initializeApp } from "https://www.gstatic.com/firebasejs/10.11.1/firebase-app.js";
import { getAuth } from "https://www.gstatic.com/firebasejs/10.11.1/firebase-auth.js";
import { getFirestore } from "https://www.gstatic.com/firebasejs/10.11.1/firebase-firestore.js";
import { getMessaging, getToken, onMessage } from "https://www.gstatic.com/firebasejs/10.11.1/firebase-messaging.js";


// Firebase Configuration
const firebaseConfig = {
    apiKey: "AIzaSyAhBlyXYwfLE1rXPcWRiouJfsp6gIpG894",
    authDomain: "smartq-d015b.firebaseapp.com",
    projectId: "smartq-d015b",
    storageBucket: "smartq-d015b.firebasestorage.app",
    messagingSenderId: "452644823738",
    appId: "1:452644823738:web:7a133f086ff93200b39883",
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);
const messaging = getMessaging(app);

// Request Notification Permission
export async function requestNotificationPermission() {
    try {
        const token = await getToken(messaging, { vapidKey: "YOUR_VAPID_PUBLIC_KEY" });
        if (token) {
            console.log("Notification Token:", token);
            return token;
        } else {
            console.log("No permission for notifications");
        }
    } catch (error) {
        console.error("Notification permission error:", error);
    }
}

// Listen for Incoming Messages
onMessage(messaging, (payload) => {
    console.log("Message received:", payload);
    alert(` Notification: ${payload.notification.title} - ${payload.notification.body}`);
});

export { auth, db, messaging };

