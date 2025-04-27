// auth.js

import { auth, db } from './firebase-config.js';
import { 
    createUserWithEmailAndPassword, 
    signInWithEmailAndPassword 
} from "https://www.gstatic.com/firebasejs/10.11.1/firebase-auth.js";
import { setDoc, doc } from "https://www.gstatic.com/firebasejs/10.11.1/firebase-firestore.js";
import { setPersistence, browserLocalPersistence, browserSessionPersistence } from "https://www.gstatic.com/firebasejs/10.11.1/firebase-auth.js";

// UI Elements
const loginForm = document.getElementById("login-form");
const registerForm = document.getElementById("register-form");
const errorMessage = document.getElementById("error-message");
const registerLink = document.getElementById("register-link");
const loginLink = document.getElementById("login-link");

// Switching Between Forms
registerLink.addEventListener("click", (e) => {
    e.preventDefault();
    document.getElementById("login-form-container").style.display = "none";
    document.getElementById("register-form-container").style.display = "block";
    clearErrorMessage();
});

loginLink.addEventListener("click", (e) => {
    e.preventDefault();
    document.getElementById("register-form-container").style.display = "none";
    document.getElementById("login-form-container").style.display = "block";
    clearErrorMessage();
});

// Clear Error Messages
function clearErrorMessage() {
    errorMessage.style.display = "none";
    errorMessage.textContent = "";
}

// Display Error Messages
function displayErrorMessage(message) {
    errorMessage.style.display = "block";
    errorMessage.textContent = message;
}

// Login
loginForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const rememberMe = document.getElementById("rememberMe").checked;

    clearErrorMessage();

    // Set persistence based on checkbox
    const persistence = rememberMe ? browserLocalPersistence : browserSessionPersistence;

    setPersistence(auth, persistence)
        .then(() => {
            return signInWithEmailAndPassword(auth, email, password);
        })
        .then(() => {
            window.location.href = "/views/admin/dashboard.html";
        })
        .catch((error) => {
            // ... existing error handling ...
        });
});

// Register
registerForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const name = document.getElementById("name").value;
    const email = document.getElementById("reg-email").value;
    const password = document.getElementById("reg-password").value;
    const confirmPassword = document.getElementById("confirm-password").value;

    clearErrorMessage();

    if (password !== confirmPassword) {
        displayErrorMessage("Passwords do not match!");
        return;
    }

    try {
        const userCredential = await createUserWithEmailAndPassword(auth, email, password);
        const user = userCredential.user;

        // Store Admin in Firestore
        await setDoc(doc(db, "admins", user.uid), {
            name: name,
            email: email
        });

        window.location.href = "/views/admin/dashboard.html"; // Redirect to admin panel
    } catch (error) {
        let errorMsg = error.message;
        if (error.code === 'auth/email-already-in-use') errorMsg = "Email is already in use!";
        if (error.code === 'auth/weak-password') errorMsg = "Weak password! Use at least 6 characters.";
        displayErrorMessage(errorMsg);
    }
});
