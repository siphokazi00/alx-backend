import express from 'express';
import { promisify } from 'util';
import redis from 'redis';
import kue from 'kue';

// Initialize the Express app and Kue queue
const app = express();
const queue = kue.createQueue();
const PORT = 1245;

// Create a Redis client and promisify its get/set methods
const client = redis.createClient();
const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);

// Initialize available seats and reservation flag
const INITIAL_AVAILABLE_SEATS = 50;
let reservationEnabled = true;

// Set the initial number of available seats
async function initializeSeats() {
    await setAsync('available_seats', INITIAL_AVAILABLE_SEATS);
}

// Function to reserve seats
async function reserveSeat(number) {
    await setAsync('available_seats', number);
}

// Function to get current available seats
async function getCurrentAvailableSeats() {
    const seats = await getAsync('available_seats');
    return seats ? parseInt(seats, 10) : 0;
}

// Initialize available seats on startup
initializeSeats();

// Route to get available seats
app.get('/available_seats', async (req, res) => {
    const availableSeats = await getCurrentAvailableSeats();
    res.json({ numberOfAvailableSeats: availableSeats.toString() });
});

// Route to reserve a seat
app.get('/reserve_seat', async (req, res) => {
    if (!reservationEnabled) {
        return res.json({ status: 'Reservations are blocked' });
    }

    // Create a job in the queue
    const job = queue.create('reserve_seat').save((err) => {
        if (err) {
            return res.json({ status: 'Reservation failed' });
        }
        return res.json({ status: 'Reservation in process' });
    });
});

// Process the reservation queue
queue.process('reserve_seat', async (job, done) => {
    try {
        const currentAvailableSeats = await getCurrentAvailableSeats();
        if (currentAvailableSeats <= 0) {
            reservationEnabled = false;
            return done(new Error('Not enough seats available'));
        }

        // Decrease the number of available seats
        const newAvailableSeats = currentAvailableSeats - 1;
        await reserveSeat(newAvailableSeats);

        if (newAvailableSeats === 0) {
            reservationEnabled = false; // Disable reservations
        }

        console.log(`Seat reservation job ${job.id} completed`);
        done();
    } catch (error) {
        console.error(`Seat reservation job ${job.id} failed: ${error.message}`);
        done(error);
    }
});

// Route to trigger processing of the queue
app.get('/process', (req, res) => {
    res.json({ status: 'Queue processing' });
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
