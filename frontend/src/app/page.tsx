"use client";
import { useTTS } from "@cartesia/cartesia-js/react";
import SenateRoom from "@/components/SenateRoom";
import { useEffect, useState } from "react";

import { Clauses, StartSim } from "./bill";

const voiceToKeyMap = new Map<string, string>();
voiceToKeyMap.set("Boozman", "77b0d4ff-228a-42cf-9fb9-f92280e7a4eb");
voiceToKeyMap.set("McConnell", "3763537f-21f8-42a3-a9b4-5baf2721f7e5");
voiceToKeyMap.set("Stabenow", "1bbfa288-2a6f-41c4-aaa6-0635947c0f54");

export default function Home() {
	const [clauses, setClauses] = useState<string[]>([]);
	const [activeClause, setActiveClause] = useState(-1);
	const [speaker, setActiveSpeaker] = useState(undefined);
	const [dialogue, setActiveDialogue] = useState(undefined);
	const [hasStarted, setHasStarted] = useState(false);
	const tts = useTTS({
		apiKey: "06f02b5d-3c2a-4f4b-8ab6-6d40d392e602",
		sampleRate: 44100,
	});

	useEffect(() => {
		const handleClauseChange = async () => {
			try {
				if (speaker && dialogue) {
					const response = await tts.buffer({
						model_id: "sonic-english",
						voice: {
							mode: "id",
							id: voiceToKeyMap.get(speaker),
						},
						transcript: dialogue,
					});
					await tts.play();
				}
			} catch {
				console.error("Error in speech");
			}
		};
		handleClauseChange();
	}, [speaker, dialogue]);

	return (
		<div style={{ display: "flex", maxWidth: "100%" }}>
			<div style={{ width: "70%" }}>
				<SenateRoom activeSpeaker={speaker} />
			</div>
			<div
				style={{
					backgroundColor: "#384F8B",
					minHeight: "100vh",
					height: "100%",
					width: "30%",
				}}
			>
				{hasStarted ? (
					<Clauses
						clauses={clauses}
						setActiveClause={setActiveClause}
					/>
				) : (
					<StartSim
						setHasStarted={setHasStarted}
						setClauses={setClauses}
					/>
				)}
			</div>
		</div>
	);
}
