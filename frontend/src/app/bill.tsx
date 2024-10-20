import "./bill.css";

import { useTTS } from "@cartesia/cartesia-js/react";
import { useState } from "react";

// import { cartesiaConnection } from "@/components/TestCartesia";

// const ws = StartWebSocket();

const difflib = require("difflib");
export function generateDiffHtml(string1, string2) {
	console.log(string1, string2);
	// Preprocessing
	var s1 = string1.split("\n").map((line) => line + "\n");
	var s2 = string2.split("\n").map((line) => line + "\n");
	let d = new difflib.Differ();
	let diff = d.compare(s1, s2);
	// Convert iterator to an array
	let diffArray = Array.from(diff);
	function diffToHtml(diff) {
		return diff
			.map((line) => {
				if (line.startsWith("- ")) {
					return `<span style="background-color: #F0AFA3;">${line.slice(
						2
					)}</span>`;
				} else if (line.startsWith("+ ")) {
					return `<span style="background-color: #DDFFDD;">${line.slice(
						2
					)}</span>`;
				} else if (line.startsWith("  ")) {
					return line.slice(2);
				}
				return "";
			})
			.join("<br>\n");
	}
	let htmlContent = diffToHtml(diffArray);
	return htmlContent;
}

async function PostStartSim(): Promise<string[]> {
	const clauses_response = await fetch("http://localhost:8080/start_sim", {
		method: "GET",
	});

	const clauses_json = await clauses_response.json();

	const clauses = clauses_json["clauses"];

	return clauses;
}

// function StartWebSocket() {
// 	const ws = new WebSocket("ws://localhost:8765");

// 	ws.onopen = () => {
// 		console.log("connected");
// 	};

// 	ws.onmessage = (message) => {
// 		console.log(message);
// 		const payload = JSON.parse(message.data);
// 		const clauseId = payload["clause_id"];
// 		const dialogue = payload["dialogue"];
// 		const speaker = payload["speaker"];
// 		const clause = payload["clause"];

// 		clauseIdToQueue[clauseId].push(payload);

// 		console.log(message);
// 	};

// 	ws.onclose = () => {
// 		console.log("disconnected");
// 	};

// 	return ws;
// }

function CreateClauses(
	clauses: string[],
	setActiveClause: (activeClause: number) => void,
	clauseIdToQueue: any,
	setClauses: (clauses: string[]) => void
) {
	const clauses_divs = [];
	const voiceToKeyMap = new Map<string, string>();
	voiceToKeyMap.set("John Boozman", "77b0d4ff-228a-42cf-9fb9-f92280e7a4eb");
	voiceToKeyMap.set("Mitch McConnell", "3763537f-21f8-42a3-a9b4-5baf2721f7e5");
	voiceToKeyMap.set("Debbie Stabenow", "1bbfa288-2a6f-41c4-aaa6-0635947c0f54");
	voiceToKeyMap.set("Cory Booker", "1bbfa288-2a6f-41c4-aaa6-0635947c0f54");
	voiceToKeyMap.set("Mike Braun", "1bbfa288-2a6f-41c4-aaa6-0635947c0f54");
	voiceToKeyMap.set("Amy Klobuchar", "1bbfa288-2a6f-41c4-aaa6-0635947c0f54");

	for (let i = 0; i < clauses.length; i++) {
		const clause = clauses[i];

		const onClick = async () => {
			setActiveClause(i);
		};

		const tts = useTTS({
			apiKey: "06f02b5d-3c2a-4f4b-8ab6-6d40d392e602",
			sampleRate: 44100,
		});

		const handlePlay = async (dialogue, voiceId) => {
			console.log("============== voiceId", voiceId);
			console.log("============== dialogue", dialogue);
			// Begin buffering the audio.
			const response = await tts.buffer({
				model_id: "sonic-english",
				voice: {
					mode: "id",
					id: voiceId,
				},
				transcript: dialogue,
			});

			// Immediately play the audio. (You can also buffer in advance and play later.)
			await tts.play();
		};

		const [htmlContent, setHtmlContent] = useState(clause);
		// let htmlContent = clause;

		clauses_divs.push(
			<div
				className="bill-section"
				onClick={() => {
					// onClick();
					const mostRecentClause =
						clauseIdToQueue[i][clauseIdToQueue[i].length - 1];
					console.log(
						"============== most recent clause",
						mostRecentClause["dialogue"],
						mostRecentClause["senator"]
					);
					console.log(...clauses.slice(0, i));

					// cartesiaConnection(mostRecentClause["dialogue"], voiceToKeyMap.get(mostRecentClause["senator"] )?? '');
					handlePlay(
						mostRecentClause["dialogue"],
						voiceToKeyMap.get(mostRecentClause["senator"]) ??
							"1bbfa288-2a6f-41c4-aaa6-0635947c0f54"
					);
				}}
				key={i}
				dangerouslySetInnerHTML={{ __html: htmlContent }}
			></div>
		);
	}

	return clauses_divs;
}

export function Clauses({
	clauses,
	setActiveClause,
	clauseIdToQueue,
	setClauses,
}: {
	clauses: string[];
	setActiveClause: (activeClause: number) => void;
	dialogue: string;
	speaker: string;
	clauseIdToQueue: any;
	setClauses: (clauses: string[]) => void;
}) {
	const clauses_divs = CreateClauses(
		clauses,
		setActiveClause,
		clauseIdToQueue,
		setClauses
	);

	return (
		<div>
			<h1 id="bill-section-title">proposed bill</h1>
			{clauses_divs}
		</div>
	);
}

export function StartSim({
	setHasStarted,
	setClauses,
	clauseIdToQueue,
}: {
	setHasStarted: (hasStarted: boolean) => void;
	setClauses: (clauses: string[]) => void;
	clauseIdToQueue: Array<Array<any>>;
}) {
	const startSim = async () => {
		const clauses = await PostStartSim();

		for (let i = 0; i < clauses.length; i++) {
			console.log("adding to clause_ids");
			clauseIdToQueue[i] = new Array<any>();
			clauseIdToQueue[i].push(clauses[i]);
		}

		setClauses(clauses);
		setHasStarted(true);
	};

	return (
		<div id="start-sim-section">
			<h1 id="bill-section-title">let the senate begin!</h1>

			<button
				onClick={() => startSim()}
				type="button"
				id="start-button"
				className="text-gray-900
                           bg-white
                           border 
                           border-gray-300
                           focus:outline-none
                           hover:bg-gray-100
                           font-medium
                           rounded-lg
                           text-sm
                           px-5
                           py-2.5
                           me-2
                           mb-2"
			>
				start
			</button>
		</div>
	);
}
