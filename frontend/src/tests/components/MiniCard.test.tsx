import { expect, test } from "vitest";
import { render } from "@testing-library/react";
import MiniCard from "../../components/MiniCard/MiniCard";

test("Populated detail panel renders correctly.", async () => {
    const { findByTestId } = render(
        <MiniCard
            backgroundColor="#3b5fe2"
            iconBackgroundColor="#2f48a2"
            mainText="R1000"
            subText="Budget remaining"
            iconName="wallet2"
            directLink="/budgets"
        />
	);

	const card = await findByTestId("sa-mini-card");
	expect(card).toMatchSnapshot();
});