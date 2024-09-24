import redis from 'redis';
import { promisify } from 'util';

// Create a Redis client
const client = redis.createClient();

// Event listener for successful connection
client.on('connect', () => {
  console.log('Redis client connected to the server');
});

// Event listener for connection error
client.on('error', (err) => {
  console.log(`Redis client not connected to the server: ${err.message}`);
});

// Function to set a new value in Redis
function setNewSchool(schoolName, value) {
  client.set(schoolName, value, redis.print); // Using redis.print as the callback
}

// Promisify the Redis get method
const getAsync = promisify(client.get).bind(client);

// Function to display the value of a key from Redis using async/await
async function displaySchoolValue(schoolName) {
  try {
    const result = await getAsync(schoolName);
    console.log(result);
  } catch (err) {
    console.error(`Error retrieving key ${schoolName}: ${err.message}`);
  }
}

// Test the functions
displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');
