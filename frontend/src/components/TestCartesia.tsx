import Cartesia from "@cartesia/cartesia-js";

const audioContext = new window.AudioContext();

function base64ToArrayBuffer(base64: string) {
	const binaryString = window.atob(base64);
	const len = binaryString.length;
	const bytes = new Uint8Array(len);

	for (let i = 0; i < len; i += 3) {
		bytes[i] = binaryString.charCodeAt(i);
        bytes[i + 1] = binaryString.charCodeAt(i + 1);
        bytes[i + 2] = binaryString.charCodeAt(i + 2);
	}


	return bytes.buffer;
}

function convertToAudioBuffer(
	base64String: string,
	sampleRate = 44100,
	channels = 1
) {
	// Decode base64 string into ArrayBuffer
	const arrayBuffer = base64ToArrayBuffer(base64String);
	return arrayBuffer;
}

// Function to play PCM f32le audio using the Web Audio API
async function playPCMFromBase64(
	arrayBuffer: Array<any>,
	sampleRate = 44100,
	channels = 1
) {
	// Convert ArrayBuffer to Float32Array
	const pcmData = new Float32Array(arrayBuffer);

    console.log(pcmData);

	// Create an AudioContext
	const audioContext = new window.AudioContext();

	// Calculate the number of samples
	const numSamples = pcmData.length / channels;

	// Create an AudioBuffer with the decoded PCM data
	const audioBuffer = audioContext.createBuffer(
		channels,
		numSamples,
		sampleRate
	);

	// Fill the AudioBuffer with the PCM data
	for (let channel = 0; channel < channels; channel++) {
		const nowBuffering = audioBuffer.getChannelData(channel);
		for (let i = 0; i < nowBuffering.length; i++) {
			nowBuffering[i] = pcmData[i * channels + channel];
		}
	}

	// Create an AudioBufferSourceNode to play the AudioBuffer
	const source = audioContext.createBufferSource();
	source.buffer = audioBuffer;

	// Connect the source to the audio context's destination (speakers)
	source.connect(audioContext.destination);

	// Start playback
	source.start();
}

export async function cartesiaConnection() {
	const cartesia = new Cartesia({
		apiKey: "06f02b5d-3c2a-4f4b-8ab6-6d40d392e602",
	});

	// Initialize the WebSocket. Make sure the output format you specify is supported.
	const websocket = cartesia.tts.websocket({
		container: "raw",
		encoding: "pcm_f32le",
		sampleRate: 44100,
	});

	try {
		await websocket.connect();
	} catch (error) {
		console.error(`Failed to connect to Cartesia: ${error}`);
	}

	// Create a stream.
	const response = websocket.send({
		model_id: "sonic-english",
		voice: {
			mode: "id",
			id: "a0e99841-438c-4a64-b679-ae501e7d6091",
		},
		transcript:
			"Arkansans planning travel abroad should find many of the preparation processes easier to navigate than in recent years. READ my latest column on the updates and resources that should reduce stress and increase passport application and renewal options.!",
		// The WebSocket sets output_format on your behalf.
	});

    let chunks = [];
    let setFirstChunk = false;
    let firstChunk = null;

	// Access the raw messages from the WebSocket.
	response.on("message", async (message: any) => {
        console.log(message);

        const parsedMessage = JSON.parse(message);

        if (chunks.length > 30) {
            let audioBuffer = convertToAudioBuffer(chunks.join(""));

            if (!setFirstChunk) {
                firstChunk = audioBuffer;
            } else {
                audioBuffer = new Uint8Array([...firstChunk, ...audioBuffer]);
            }

            playPCMFromBase64(audioBuffer);
            chunks = [];
            chunks.push(firstChunk);
        }

        if (parsedMessage.done) {
            console.log("done");
            console.log(chunks.length);
            const audioBuffer = convertToAudioBuffer(chunks.join(""));
            playPCMFromBase64(audioBuffer);

            console.log(audioBuffer);
        }

        chunks.push(parsedMessage.data);

	});

}
