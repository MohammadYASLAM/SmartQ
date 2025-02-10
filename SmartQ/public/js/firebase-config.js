// firebase-config.js

import { initializeApp } from "https://www.gstatic.com/firebasejs/10.11.1/firebase-app.js";
import { getAuth } from "https://www.gstatic.com/firebasejs/10.11.1/firebase-auth.js";
import { getFirestore } from "https://www.gstatic.com/firebasejs/10.11.1/firebase-firestore.js";

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

export { auth, db };
