"use client";
import "./SenateRoom.css";
import Senator from "./Senator";

export default function SenateRoom(props: any) {
	const activeSpeaker = props.activeSpeaker;

	return (
		<div id="senate-room-main-div">
			<div id="senator-male-1">
				<Senator talking={activeSpeaker == "Boozman"} />
			</div>
			<div id="senator-male-2">
				<Senator
					haircolor="black"
					talking={activeSpeaker == "McConnell"}
				/>
			</div>
			<div id="senator-female-1">
				<Senator
					haircolor="brown"
					talking={activeSpeaker == "Stabenow"}
				/>
			</div>
		</div>
	);
}
