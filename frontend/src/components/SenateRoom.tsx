"use client";
import { useCallback, useEffect, useState } from "react";
import "./SenateRoom.css";
import Senator from "./Senator";
import { useTTS } from "@cartesia/cartesia-js/react";

interface SenateRoomProps {
	dialogue: string;
	speaker: string;
}

export default function SenateRoom(props: SenateRoomProps) {
	const voiceToKeyMap = new Map<string, string>();
	voiceToKeyMap.set("Boozman", "77b0d4ff-228a-42cf-9fb9-f92280e7a4eb");
	voiceToKeyMap.set("McConnell", "3763537f-21f8-42a3-a9b4-5baf2721f7e5");
	voiceToKeyMap.set("Stabenow", "1bbfa288-2a6f-41c4-aaa6-0635947c0f54");

	const handlePlayAudio = async () => {
		const tts = useTTS({
			apiKey: "06f02b5d-3c2a-4f4b-8ab6-6d40d392e602",
			sampleRate: 44100,
		});
		const voiceId = voiceToKeyMap.get(props.speaker);
		const response = await tts.buffer({
			model_id: "sonic-english",
			voice: {
				mode: "id",
				id: voiceId,
			},
			transcript: props.dialogue,
		});

		await tts.play();
	};

	return (
		<div id="senate-room-main-div">
			<div id="senator-male-1">
				<Senator />
			</div>
			<div id="senator-male-2">
				<Senator />
			</div>
			<div id="senator-male-2">
				<Senator haircolor="black" />
			</div>
			<div id="senator-female-1">
				<Senator haircolor="brown" />
			</div>
			{/* <div id="senator-female-2">
				<Senator />
			</div> */}
			<button>click me</button>
		</div>
	);
}
