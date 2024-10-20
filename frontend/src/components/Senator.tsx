import { useEffect, useRef } from "react";
import "./Senator.css";

export default function Senator(props: any) {
	const haircolor = props.haircolor;
	const mouthElement = useRef<HTMLDivElement>(null);

	function startTalking() {
		if (mouthElement.current) {
			mouthElement.current.classList.add("mouth-talking");
		}
	}

	function stopTalking() {
		if (mouthElement.current) {
			mouthElement.current.classList.remove("mouth-talking");
		}
	}

	useEffect(() => {
		if (props.talking) {
			startTalking();
		} else {
			stopTalking();
		}
	}, []);

	return (
		<>
			<div className="wrapper">
				<div className="background-circle">
					<div className="body"></div>
				</div>
				<div className="head">
					<div
						className="ear"
						id="left"
					></div>
					<div
						className="ear"
						id="right"
					></div>
					<div
						className="hair-main"
						style={{ background: haircolor }}
					>
						<div
							className="sideburn"
							id="left"
							style={{ background: haircolor }}
						></div>
						<div
							className="sideburn"
							id="right"
							style={{ background: haircolor }}
						></div>
						<div
							className="hair-top"
							style={{ background: haircolor }}
						></div>
					</div>
					<div className="face">
						<div
							className="hair-bottom"
							style={{ background: haircolor }}
						></div>
						<div className="nose"></div>
						<div
							className="eye-shadow"
							id="left"
						>
							<div className="eyebrow"></div>
							<div className="eye"></div>
						</div>
						<div
							className="eye-shadow"
							id="right"
						>
							<div className="eyebrow"></div>
							<div className="eye"></div>
						</div>
						<div
							className="mouth"
							ref={mouthElement}
						></div>
						<div className="shadow-wrapper">
							<div className="shadow"></div>
						</div>
					</div>
				</div>
			</div>
		</>
	);
}
