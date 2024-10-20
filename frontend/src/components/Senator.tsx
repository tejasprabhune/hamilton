import "./Senator.css";

export default function Senator(props: any) {
	const haircolor = props.haircolor;
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
						<div className="mouth"></div>
						<div className="shadow-wrapper">
							<div className="shadow"></div>
						</div>
					</div>
				</div>
			</div>
		</>
	);
}
