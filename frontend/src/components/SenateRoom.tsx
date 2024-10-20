"use client";
import { useEffect, useRef } from "react";
import "./SenateRoom.css";
import Senator from "./Senator";

export default function SenateRoom(props: any) {
	const { activeSpeaker } = props;

	const boozmanRef = useRef<HTMLDivElement>(null);
	const mcconnellRef = useRef<HTMLDivElement>(null);
	const stabenowRef = useRef<HTMLDivElement>(null);
	const klobucharRef = useRef<HTMLDivElement>(null);
	const braunRef = useRef<HTMLDivElement>(null);
	const bookerRef = useRef<HTMLDivElement>(null);

	function startTalking(ref: React.RefObject<HTMLDivElement>) {
		if (ref.current) {
			ref.current.classList.add("zoom-in");
		}
	}

	function stopTalking(ref: React.RefObject<HTMLDivElement>) {
		if (ref.current) {
			ref.current.classList.remove("zoom-in");
		}
	}

	useEffect(() => {
		stopTalking(boozmanRef);
		stopTalking(mcconnellRef);
		stopTalking(stabenowRef);

		if (activeSpeaker === "Boozman") {
			startTalking(boozmanRef);
		} else if (activeSpeaker === "McConnell") {
			startTalking(mcconnellRef);
		} else if (activeSpeaker === "Stabenow") {
			startTalking(stabenowRef);
		} else if (activeSpeaker === "Klobuchar") {
			startTalking(klobucharRef);
		} else if (activeSpeaker === "Booker") {
			startTalking(bookerRef);
		} else if (activeSpeaker === "Braun") {
			startTalking(braunRef);
		}
	}, [activeSpeaker]);

	return (
		<div id="senate-room-main-div">
			<div
				id="senator-male-1"
				ref={boozmanRef}
			>
				<Senator talking={activeSpeaker == "Boozman"} />
			</div>
			<div
				id="senator-male-2"
				ref={mcconnellRef}
			>
				<Senator
					haircolor="black"
					talking={activeSpeaker == "McConnell"}
				/>
			</div>
			<div
				id="senator-female-1"
				ref={stabenowRef}
			>
				<Senator
					haircolor="brown"
					talking={activeSpeaker == "Stabenow"}
				/>
			</div>

			<div
				id="senator-female-2"
				ref={klobucharRef}
			>
				<Senator talking={activeSpeaker == "Klobuchar"} />
			</div>

			<div
				id="senator-female-3"
				ref={braunRef}
			>
				<Senator
					talking={activeSpeaker == "Braun"}
					haircolor="black"
				/>
			</div>

			<div
				id="senator-female-4"
				ref={bookerRef}
			>
				<Senator
					talking={activeSpeaker == "Booker"}
					haircolor="brown"
				/>
			</div>
		</div>
	);
}
