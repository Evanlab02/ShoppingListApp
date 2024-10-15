import { beforeEach, expect, test, vi } from "vitest";
import { fireEvent, render } from "@testing-library/react";
import Card from "../../components/Card/Card";

beforeEach(() => {
	document.getElementsByTagName("html")[0].innerHTML = "";
});

test("Basic Card renders correctly.", async () => {
    const { findByTestId } = render(
        <Card
            backgroundColor="#602786"
            iconBackgroundColor="#562f6f"
            mainText="Test Card"
        />
	);

	const card = await findByTestId("sa-card");
	expect(card).toMatchSnapshot();
});

test("Advanced Card renders correctly.", async () => {
    const fn = vi.fn();

    const { findByTestId } = render(
        <Card
            backgroundColor="#602786"
            iconBackgroundColor="#562f6f"
            mainText="Advanced Card"
            directLink="/hi/"
            iconName="wallet2"
            subText="Hello World!"
            onClick={fn}
        />
	);

	const card = await findByTestId("sa-card");
	expect(card).toMatchSnapshot();

    const click = await findByTestId("sa-card-click");
    fireEvent.click(click);
    expect(fn).toBeCalledTimes(1);
});