import { useParams } from 'react-router-dom';

function DisasterPlanDisplay() {
    const { risk } = useParams();

    return (
        <div>
            <h1>Disaster Plan for {risk}</h1>
            <p>This is where the generated disaster plan for {risk} will be displayed.</p>
        </div>
    )
}

export default DisasterPlanDisplay;