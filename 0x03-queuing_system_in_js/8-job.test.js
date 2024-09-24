import kue from 'kue';
import createPushNotificationsJobs from './8-job.js';
import { expect } from 'chai';

describe('createPushNotificationsJobs', () => {
  let queue;

  before(() => {
    // Create a new Kue queue and enter test mode
    queue = kue.createQueue();
    queue.testMode.enter();
  });

  after(() => {
    // Clear the queue and exit test mode
    return queue.testMode.exit();
  });

  it('should throw an error if jobs is not an array', () => {
    expect(() => createPushNotificationsJobs({}, queue)).to.throw(Error, 'Jobs is not an array');
  });

  it('should create new jobs in the queue', () => {
    const jobs = [
      {
        phoneNumber: '4153518780',
        message: 'This is the code 1234 to verify your account'
      },
      {
        phoneNumber: '4153518781',
        message: 'This is the code 4562 to verify your account'
      }
    ];

    createPushNotificationsJobs(jobs, queue);

    // Check the jobs in the queue
    const jobIds = queue.testMode.jobs.map(job => job.id);
    expect(jobIds.length).to.equal(2); // Expecting two jobs to be created
  });

  afterEach(() => {
    // Clear the queue before the next test
    queue.testMode.clear();
  });
});
