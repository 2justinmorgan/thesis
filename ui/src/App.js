import React, { useState } from 'react';
import {
  ScatterChart,
  Scatter,
  XAxis,
  YAxis,
  ZAxis,
} from 'recharts';

const App = () => {
    const data01 = React.useMemo(
        () => require("./data").points.slice(0,10),
        []
    );

    const [ data, setData ] = useState(data01);

    return (
        <ScatterChart width={500} height={400}>
            <XAxis type="number" dataKey="x" />
            <YAxis type="number" dataKey="y" />
            <ZAxis range={[0]} />
            <Scatter data={data} fill="green" lineJointType="natural" line />
        </ScatterChart>
    );
}

export default App;

