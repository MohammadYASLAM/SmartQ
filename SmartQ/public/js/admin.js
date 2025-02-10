// admin.js
firebase.auth().onAuthStateChanged((user) => {
    if (user) {
      // If admin is logged in, show the dashboard
      document.getElementById("admin-dashboard").style.display = "block";
      document.getElementById("auth-page").style.display = "none";
    } else {
      // Redirect to login page if not logged in
      document.getElementById("admin-dashboard").style.display = "none";
      document.getElementById("auth-page").style.display = "block";
    }
  });
  
  function loginAdmin() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    
    firebase.auth().signInWithEmailAndPassword(email, password)
      .then((userCredential) => {
        console.log("Admin logged in:", userCredential.user);
      })
      .catch((error) => {
        console.error("Error logging in:", error.message);
      });
  }
  
  function registerAdmin() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    
    firebase.auth().createUserWithEmailAndPassword(email, password)
      .then((userCredential) => {
        console.log("Admin registered:", userCredential.user);
      })
      .catch((error) => {
        console.error("Error registering:", error.message);
      });
  }
  
  function logoutAdmin() {
    firebase.auth().signOut()
      .then(() => {
        console.log("Admin logged out");
      })
      .catch((error) => {
        console.error("Error logging out:", error.message);
      });
  }

  
  // admin.js (continued)
function createQueue(queueName) {
    const queueRef = db.collection("queues").doc();
    queueRef.set({
      name: queueName,
      status: "active",
      users: [],
      currentPosition: 1,
      estimatedWaitTime: 0,
      waitTimes: [],
      createdAt: firebase.firestore.FieldValue.serverTimestamp(),
      lastUpdate: firebase.firestore.FieldValue.serverTimestamp()
    }).then(() => {
      console.log("Queue created successfully");
    }).catch((error) => {
      console.error("Error creating queue:", error.message);
    });
  }
  
  function addUserToQueue(queueId, userId, userName) {
    const queueRef = db.collection("queues").doc(queueId);
    queueRef.update({
      users: firebase.firestore.FieldValue.arrayUnion({
        userId: userId,
        position: queueRef.data().currentPosition + 1
      }),
      currentPosition: firebase.firestore.FieldValue.increment(1)
    }).then(() => {
      console.log("User added to the queue");
    }).catch((error) => {
      console.error("Error adding user:", error.message);
    });
  }
  