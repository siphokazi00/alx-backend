import kue from 'kue';

// Create a Kue queue
const queue = kue.createQueue();

// Define job data
const jobData = {
  phoneNumber: '1234567890',
  message: 'This is a push notification message',
};

// Create a job in the 'push_notification_code' queue
const job = queue.create('push_notification_code', jobData)
  .save((err) => {
    if (!err) {
      console.log(`Notification job created: ${job.id}`);
    } else {
      console.error('Failed to create job:', err);
    }
  });

// Event listener for job completion
job.on('complete', () => {
  console.log('Notification job completed');
});

// Event listener for job failure
job.on('failed', () => {
  console.log('Notification job failed');
});
