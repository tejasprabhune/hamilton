"use client";

import { useState } from "react";

import { Clauses, StartSim } from "./bill";

export default function Home() {

    const [clauses, setClauses] = useState<string[]>([]);
    const [activeClause, setActiveClause] = useState(-1);
    const [hasStarted, setHasStarted] = useState(false);

	return (
		<div style={{ display: "flex", maxWidth: "100%" }}>
			<div style={{ width: "70%" }}>component 1</div>
			<div style={{ backgroundColor: "#384F8B", minHeight: "100vh", height: "100%", width: "30%" }}>
                { hasStarted ? <Clauses clauses={ clauses } 
                                          setActiveClause={ setActiveClause } />
                                : <StartSim setHasStarted={ setHasStarted } setClauses={ setClauses } /> }
            </div>
		</div>
	);
}
