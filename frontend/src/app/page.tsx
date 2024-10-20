"use client";
import { useTTS } from "@cartesia/cartesia-js/react";
import SenateRoom from "@/components/SenateRoom";
import { useEffect, useState } from "react";

import { Clauses, StartSim } from "./bill";

export default function Home() {
	const [clauses, setClauses] = useState<string[]>([]);
	const [activeClause, setActiveClause] = useState(-1);
	const [speaker, setActiveSpeaker] = useState("Boozman");
	const [dialogue, setActiveDialogue] = useState("Hi there");
	const [hasStarted, setHasStarted] = useState(false);
	const tts = useTTS({
		apiKey: process.env.CARTESIA_API_KEY,
		sampleRate: 44100,
	});

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
						tts={tts}
						speaker={speaker}
						dialogue={dialogue}
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
