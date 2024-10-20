"use client";
import { useTTS } from "@cartesia/cartesia-js/react";
import SenateRoom from "@/components/SenateRoom";
import { useEffect, useState } from "react";

import { Clauses, generateDiffHtml, StartSim } from "./bill";

let clauseIdToQueue = new Array<Array<any>>();

function StartWebSocket(setClauses: (clauses: string[]) => void) {
	const ws = new WebSocket("ws://localhost:8765");

	ws.onopen = () => {
		console.log("connected");
	};

	ws.onmessage = (message) => {
		console.log(message);
		const payload = JSON.parse(message.data);

		const event = payload["event"];

		const clauseId = payload["clause_id"];
		const dialogue = payload["dialogue"];
		const speaker = payload["senator"];
		const clause = payload["clause"];

		if (clauseIdToQueue[clauseId] === undefined) {
			clauseIdToQueue[clauseId] = [];
		}

		const htmlDiff = generateDiffHtml(
			clauseIdToQueue[clauseId][clauseIdToQueue[clauseId].length - 1],
			clause
		);

		console.log("HTML DIFF ===========================");
		console.log(htmlDiff);
		let current_clauses = new Array<string>();
		for (let i = 0; i < current_clauses.length; i++) {
			current_clauses.push(clauseIdToQueue[i][clauseIdToQueue[i].length - 1]);
		}
		setClauses(current_clauses);
		clauseIdToQueue[clauseId].push(payload);
	};

	ws.onclose = () => {
		console.log("disconnected");
	};

	return ws;
}

export default function Home() {
	const [clauses, setClauses] = useState<string[]>([]);
	const [activeClause, setActiveClause] = useState(-1);
	const [speaker, setActiveSpeaker] = useState("Boozman");
	const [dialogue, setActiveDialogue] = useState("Hi there");
	const [hasStarted, setHasStarted] = useState(false);

	useEffect(() => {
		const ws = StartWebSocket(setClauses);
	}, []);

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
						speaker={speaker}
						dialogue={dialogue}
						clauseIdToQueue={clauseIdToQueue}
						setClauses={setClauses}
					/>
				) : (
					<StartSim
						setHasStarted={setHasStarted}
						setClauses={setClauses}
						clauseIdToQueue={clauseIdToQueue}
					/>
				)}
			</div>
		</div>
	);
}
