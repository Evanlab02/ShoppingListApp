import React from "react";
import { DetailPanelProps } from "./helpers/interfaces";
import "./styles/DetailPanel.scss"

/**
 * Detail panel component.
 * 
 * @returns Detail panel component
 */
export default function DetailPanel(props: DetailPanelProps) {

    const { records } = props;

    const renderedRecentItems = records.map((record, index) => {
        return (
            <React.Fragment key={`${record.name}-${record.price}-${index}`}>
                <hr />
                <div className="recent-item">
                    <h4>{record.name}</h4>
                    <h4>R{record.price}</h4>
                </div>
            </React.Fragment>
        );
    });

    return (
        <div className="detail-panel" data-testid="sa-detail-panel">
            <h4>Recent Items</h4>
            {renderedRecentItems}
        </div>
    );
}