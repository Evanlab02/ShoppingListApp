import { DashboardCurrent, DashboardHistory, RecentItems } from "../../helpers/apiInterfaces";

export const DASHBOARD_CURRENT_MOCK: DashboardCurrent = {
    total: 10,
    average_item_price: 80,
    budget_remaining: 150,
    total_price: 300
}

export const DASHBOARD_HISTORY_MOCK: DashboardHistory = {
    labels: [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
    ],
    data: [
        {
            label: "Price",
            data: [65, 59, 80, 81, 56, 55],
        },
        {
            label: "Budget",
            data: [28, 48, 40, 19, 86, 27],
        }
    ]
}

export const DASHBOARD_RECENT_ITEMS_MOCK: RecentItems = {
    items: [
        {name: "1", price: 100},
        {name: "2", price: 200},
        {name: "3", price: 300},
        {name: "4", price: 400},
        {name: "5", price: 500}
    ]
}