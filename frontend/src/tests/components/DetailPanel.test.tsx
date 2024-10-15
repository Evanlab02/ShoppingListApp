import { beforeEach, expect, test } from "vitest";
import { render } from "@testing-library/react";
import DetailPanel from "../../components/DetailPanel/DetailPanel";

beforeEach(() => {
	document.getElementsByTagName("html")[0].innerHTML = "";
});

test("Empty detail panel renders correctly.", async () => {
    const { findByTestId } = render(
        <DetailPanel
            records={[]}
        />
	);

	const panel = await findByTestId("sa-detail-panel");
	expect(panel).toMatchSnapshot();
});

test("Populated detail panel renders correctly.", async () => {
    const { findByTestId } = render(
        <DetailPanel
            records={[
                {name: "1", price: 100},
                {name: "2", price: 200},
                {name: "3", price: 300},
                {name: "4", price: 400},
                {name: "5", price: 500}
            ]}
        />
	);

	const panel = await findByTestId("sa-detail-panel");
	expect(panel).toMatchSnapshot();
});