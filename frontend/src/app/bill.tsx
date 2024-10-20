import './bill.css';

const ws = StartWebSocket();

async function PostStartSim() : Promise<string[]> {
    const clauses_response = await fetch("http://localhost:8080/start_sim", {
        method: "GET",
    });

    const clauses_json = await clauses_response.json();

    const clauses = clauses_json["clauses"];

    return clauses;
}

function StartWebSocket() {
    const ws = new WebSocket("ws://localhost:8081");

    ws.onopen = () => {
        console.log("connected");
    }

    ws.onmessage = (message) => {
        console.log(message);
    }

    ws.onclose = () => {
        console.log("disconnected");
    }

    return ws;
}

function CreateClauses(clauses: string[], setActiveClause: (activeClause: number) => void) {
    const clauses_divs = [];

    for (let i = 0; i < clauses.length; i++) {
        const clause = clauses[i];

        const onClick = () => {
            setActiveClause(i);
        }

        clauses_divs.push(
            <div className="bill-section" onClick={onClick} key={i} dangerouslySetInnerHTML={{__html: clause}}>
            </div>
        );
    }

    return clauses_divs;
}

export function Clauses({ clauses, setActiveClause }: { clauses: string[], setActiveClause: (activeClause: number) => void }) {
    const clauses_divs = CreateClauses(clauses, setActiveClause);

    return (
        <div>
            <h1 id="bill-section-title">proposed bill</h1>
            {clauses_divs}
        </div>
    )
}

export function StartSim({ setHasStarted, setClauses }: { setHasStarted: (hasStarted: boolean) => void, setClauses: (clauses: string[]) => void }) {

    
    const startSim = async () => {
        const clauses = await PostStartSim();

        setClauses(clauses);
        setHasStarted(true);
    }

    return (
        <div id="start-sim-section">
            <h1 id="bill-section-title">let the senate begin!</h1>

            <button onClick={() => startSim()} type="button" id="start-button" 
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
                           mb-2">start</button>
        </div>
    )
}
