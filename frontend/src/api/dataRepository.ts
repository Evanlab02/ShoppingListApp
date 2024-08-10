import { DashboardCurrent, DashboardHistory, RecentItems } from "../helpers/apiInterfaces";

export default class DataRepo {
    contentType = "";

    constructor() {
        this.contentType = "application/json";
    }

    async getDashboardCurrent(): Promise<DashboardCurrent> {
        const response = await fetch("/apis/shopping/api/v1/dashboard/overview",
            {
                method: "GET",
                headers: {
                    "Content-Type": this.contentType,
                    "Accept": "application/json"
                }
            }
        );

        if (response.status == 401) {
            window.location.href = "/";
        }

        const data = await response.json();
        return data;
    }

    async getDashboardHistory(): Promise<DashboardHistory> {
        const response = await fetch("/apis/shopping/api/v1/dashboard/history",
            {
                method: "GET",
                headers: {
                    "Content-Type": this.contentType,
                    "Accept": "application/json"
                }
            }
        );

        if (response.status == 401) {
            window.location.href = "/";
        }

        const data = await response.json();
        return data;
    }

    async getRecentItems(): Promise<RecentItems> {
        const response = await fetch("/apis/shopping/api/v1/dashboard/recent/items",
            {
                method: "GET",
                headers: {
                    "Content-Type": this.contentType,
                    "Accept": "application/json"
                }
            }
        );

        if (response.status == 401) {
            window.location.href = "/";
        }

        const data = await response.json();
        return data;
    }
}