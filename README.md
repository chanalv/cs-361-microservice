# cs-361-microservice

COMMUNICATION CONTRACT

How to REQUEST & RECEIVE Data from the Microservice

As a general overview, the microservice works by receiving a search term (e.g., '401(k)') as a string from your individual project. The microservice then calls the English Wikipedia Search API using the provided search term to receive data in response in a JSON format that contains the title of the Wikipedia article for '401(k)' and the content of the introduction section. This data in a JSON format is then returned to your individual project.

The microservice communicates between server and client using ZeroMQ sockets (https://zeromq.org/). Because your individual project (i.e., the client) is running on Node.js and the microservice (i.e., the server) is coded in Python, ZeroMQ was chosen as a communication pipe to allow the two programs to communicate with each other.

The microservice program is contained within a single .py file that was coded in Python 3.10. You can run the microservice program in a command line interpreter application, such as Command Prompt, by entering "python" or "python3" followed by the path to the .py file. The microservice program relies on two published libraries to run: ZeroMQ (https://zeromq.org/languages/python/) and requests (https://pypi.org/project/requests/). Both libraries will need to be installed prior to running the microservice program. The microservice program needs to be active and running in order to receive calls from your individual project.

The first step for requesting data from the microservice is to install ZeroMQ for Node (https://zeromq.org/languages/nodejs/). The provided link provides some instruction, but you will likely need to navigate to the root folder containing the files for your program, and enter some variation of "npm install zeromq@6.0.0-beta.6" into your console.

The next step is wherever in your program you want to request data from the microservice, you want to open a ZeroMQ client socket and then connect with the server socket. ZeroMQ provides the following documentation for getting started:
https://zeromq.org/get-started/?language=nodejs&library=zeromqjs#

Specifically, you can adapt the example code provided for the "Hello World client". The microservice/server will run on 'tcp://localhost:5555', so you don't need to modify sock.connect('tcp://localhost:5555').

Here is an example of how you can modify the example code to make a call to the microservice:

	//  individual project client
	const zmq = require('zeromq');

	async function runClient() {
		console.log('Connecting to hello world server...');

		//  Socket to talk to server
		const sock = new zmq.Request();
		sock.connect('tcp://localhost:5555');

		await sock.send('401(k)');
		const [result] = await sock.receive();
		console.log(JSON.parse(result));
		}
	}

	runClient();

In this example call, the line
		
	await sock.send('401(k))');

will send the search term '401(k)' to the microservice/server. You can modify this string to send different search terms to the microservice/server.

Then, the line

	const [result] = await sock.receive();
	
will allow your individual project to receive the raw data from the microservice/server and store the data in the result variable.

Then,

	console.log(result.toJSON());
	
will convert the raw data stored in the result variable to a JSON format, and then print that information to the console.

After receiving the raw data from the microservice/server and converting it to a JSON format, hopefully it'll be easy to use the information stored within to serve whatever purpose you had planned for in your individual project.

Possible area for troubleshooting: Data is sent as bytes from the client to the server, and vice versa. Correspondingly, data may need to be converted from string to bytes when sending data to the server, and converted from bytes to JSON when using the data received from the server. I believe the example code above handles this, but I wanted to leave this troubleshooting note for future consideration.

UML sequence diagram

![UML drawio](https://user-images.githubusercontent.com/91583603/199153284-9fef73dd-cb04-4fae-a28d-ddf1a91c5fcf.svg)

