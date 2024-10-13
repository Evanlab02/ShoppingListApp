import { expect, test } from 'vitest'
import { DASHBOARD_CURRENT_MOCK } from '../mock/dataRepoMocks'
import DataRepo from '../../api/dataRepository';

test("Data repository returns current dashboard data.", async () => {
    fetchMock.mockResponseOnce(JSON.stringify(DASHBOARD_CURRENT_MOCK));

    const repo = new DataRepo();
    const data = await repo.getDashboardCurrent();

    expect(data).toStrictEqual(DASHBOARD_CURRENT_MOCK);
    expect(data.total).toEqual(10);
    expect(data.total_price).toEqual(300);
    expect(data.budget_remaining).toEqual(150);
    expect(data.average_item_price).toEqual(80);
});