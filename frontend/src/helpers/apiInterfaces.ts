export interface DashboardCurrent {
    total: number | null;
    total_price: number | null;
    budget_remaining: number | null;
    average_item_price: number | null;
}

export interface DashboardHistory {
    labels: string[];
    data: HistoryDataSet[];
}

interface HistoryDataSet {
    label: string;
    data: number[];
}

export interface RecentItems {
    items: Item[];
}

export interface Item {
    name: string;
    price: number;
}