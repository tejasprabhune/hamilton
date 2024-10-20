import { useTTS } from "@cartesia/cartesia-js/react";
import { useEffect, useState } from "react";
import dotenv from "dotenv";

dotenv.config();

interface TextToSpeechProps {
	speaker: "McConnell" | "Boozman" | "Stabenow";
	dialogue: string;
}

const voiceToKeyMap = new Map<string, string>();
voiceToKeyMap.set("Boozman", "77b0d4ff-228a-42cf-9fb9-f92280e7a4eb");
voiceToKeyMap.set("McConnell", "3763537f-21f8-42a3-a9b4-5baf2721f7e5");
voiceToKeyMap.set("Stabenow", "1bbfa288-2a6f-41c4-aaa6-0635947c0f54");

export default function TextToSpeech(props: TextToSpeechProps) {
	const tts = useTTS({
		apiKey: "06f02b5d-3c2a-4f4b-8ab6-6d40d392e602",
		sampleRate: 44100,
	});
	const handlePlay = async () => {
		const response = await tts.buffer({
			model_id: "sonic-english",
			voice: {
				mode: "id",
				id: voiceToKeyMap.get(props.speaker),
			},
			transcript: props.dialogue,
		});
		await tts.play();
	};

	useEffect(() => {
		handlePlay();
	}, []);

	return <></>;
}
