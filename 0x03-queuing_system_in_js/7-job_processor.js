import kue from 'kue';

// Create a Kue queue
const queue = kue.createQueue({
  concurrency: 2, // Set the concurrency to process 2 jobs at a time
});

// Array of blacklisted phone numbers
const blacklistedNumbers = [
  '4153518780',
  '4153518781'
];

// Function to send notifications
const sendNotification = (phoneNumber, message, job, done) => {
  // Track job progress
  job.progress(0, 100);
  
  // Check if the phone number is blacklisted
  if (blacklistedNumbers.includes(phoneNumber)) {
    return done(new Error(`Phone number ${phoneNumber} is blacklisted`));
  }

  // If not blacklisted, track progress to 50%
  job.progress(50, 100);
  console.log(`Sending notification to ${phoneNumber}, with message: ${message}`);
  
  // Simulate sending notification (could be an API call)
  setTimeout(() => {
    // Complete the job
    done();
  }, 1000); // Simulate a delay for sending the notification
};

// Process jobs from the queue
queue.process('push_notification_code_2', (job, done) => {
  const { phoneNumber, message } = job.data;
  sendNotification(phoneNumber, message, job, done);
});

// Listen for completed jobs
queue.on('job complete', (id) => {
  console.log(`Notification job #${id} completed`);
});

// Listen for failed jobs
queue.on('job failed', (id, err) => {
  console.log(`Notification job #${id} failed: ${err.message}`);
});

// Listen for job progress
queue.on('job progress', (id, progress) => {
  console.log(`Notification job #${id} ${progress}% complete`);
});
