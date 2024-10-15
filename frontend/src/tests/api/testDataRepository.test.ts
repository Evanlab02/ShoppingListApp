import { beforeEach, expect, test } from 'vitest'
import { DASHBOARD_CURRENT_MOCK, DASHBOARD_HISTORY_MOCK, DASHBOARD_RECENT_ITEMS_MOCK } from '../mock/dataRepoMocks'
import DataRepo from '../../api/dataRepository';

beforeEach(() => {
    fetchMock.resetMocks();
})

test("Data repository returns current dashboard data.", async () => {
    fetchMock.mockResponseOnce(JSON.stringify(DASHBOARD_CURRENT_MOCK));

    const repo = new DataRepo();
    const data = await repo.getDashboardCurrent();

    expect(data).toStrictEqual(DASHBOARD_CURRENT_MOCK);
    expect(data).toMatchSnapshot(DASHBOARD_CURRENT_MOCK);
    expect(data.total).toEqual(10);
    expect(data.total_price).toEqual(300);
    expect(data.budget_remaining).toEqual(150);
    expect(data.average_item_price).toEqual(80);
});

test("Data repository returns dashboard history.", async() => {
    fetchMock.mockResponseOnce(JSON.stringify(DASHBOARD_HISTORY_MOCK));

    const repo = new DataRepo();
    const data = await repo.getDashboardHistory();

    expect(data).toStrictEqual(DASHBOARD_HISTORY_MOCK);
    expect(data).toMatchSnapshot(DASHBOARD_HISTORY_MOCK);
});

test("Data repository returns recent items.", async() => {
    fetchMock.mockResponseOnce(JSON.stringify(DASHBOARD_RECENT_ITEMS_MOCK));

    const repo = new DataRepo();
    const data = await repo.getRecentItems();

    expect(data).toStrictEqual(DASHBOARD_RECENT_ITEMS_MOCK);
    expect(data).toMatchSnapshot(DASHBOARD_RECENT_ITEMS_MOCK);
});
