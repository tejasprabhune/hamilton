import Cartesia from "@cartesia/cartesia-js";
import { useTTS } from "@cartesia/cartesia-js/react";

import { useEffect, useState } from "react";


function base64ToArrayBuffer(base64: string) {
	const binaryString = window.atob(base64);
	const len = binaryString.length;
	const bytes = new Uint8Array(len);

	for (let i = 0; i < len; i++) {
		bytes[i] = binaryString.charCodeAt(i);
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

// export async function cartesiaConnection(dialogue: string, voiceId: string) {
// 	const cartesia = new Cartesia({
// 		apiKey: "06f02b5d-3c2a-4f4b-8ab6-6d40d392e602",
// 	});
// 
// 	// Initialize the WebSocket. Make sure the output format you specify is supported.
// 	const websocket = cartesia.tts.websocket({
// 		container: "raw",
// 		encoding: "pcm_f32le",
// 		sampleRate: 44100,
// 	});
// 
// 	try {
// 		await websocket.connect();
// 	} catch (error) {
// 		console.error(`Failed to connect to Cartesia: ${error}`);
// 	}
// 
// 	// Create a stream.
// 	const response = websocket.send({
// 		model_id: "sonic-english",
// 		voice: {
// 			mode: "id",
// 			id: voiceId,
// 		},
// 		transcript: dialogue
// 		// The WebSocket sets output_format on your behalf.
// 	});
// 
//     let chunks = [];
//     let setFirstChunk = false;
//     let firstChunk = null;
// 
// 	// Access the raw messages from the WebSocket.
// 	response.on("message", async (message: any) => {
//         console.log(message);
// 
//         const parsedMessage = JSON.parse(message);
// 
// 
//         if (parsedMessage.done) {
//             console.log("done");
//             console.log(chunks.length);
//             const audioBuffer = convertToAudioBuffer(chunks.join(""));
//             playPCMFromBase64(audioBuffer);
// 
//             console.log(audioBuffer);
// 
//             chunks = [];
//         }
// 
//         chunks.push(parsedMessage.data);
// 
// 	});
// 
// }

export function CartesiaConnection(dialogue: string, voiceId: string) {

    const tts = useTTS({
		apiKey: "06f02b5d-3c2a-4f4b-8ab6-6d40d392e602",
		sampleRate: 44100,
	});

	const handlePlay = async () => {
		const response = await tts.buffer({
			model_id: "sonic-english",
			voice: {
				mode: "id",
				id: voiceId,
			},
			transcript: dialogue,
		});
		await tts.play();
	};

    await handlePlay();
}
