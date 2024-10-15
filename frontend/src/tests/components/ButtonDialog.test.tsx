import { beforeEach, expect, test, vi } from "vitest";
import { fireEvent, render } from "@testing-library/react";
import ButtonDialog from "../../components/ButtonDialog/ButtonDialog";

beforeEach(() => {
	document.getElementsByTagName("html")[0].innerHTML = "";
});

test("Button Dialog renders and functions correctly.", async () => {
	const fn = vi.fn();
    const button1Click = vi.fn();
    const button2Click = vi.fn();

    const { findByTestId } = render(
        <div data-testid="test-button-dialog">
            <ButtonDialog 
                open={true}
                onClose={fn}
                title="Testing Button Dialog"
                buttonValues={[
                    {
                        variant: "default",
                        text: "Hi",
                        onClick: button1Click
                    },
                    {
                        variant: "danger",
                        text: "Goodbye",
                        onClick: button2Click
                    }
                ]}
            />
        </div>
	);

	const btnDialog = await findByTestId("test-button-dialog");
	expect(btnDialog).toMatchSnapshot();

    
    const closeButton = await findByTestId("sa-btn-dl-close");
    fireEvent.click(closeButton);
    expect(fn).toBeCalledTimes(1);

    const customButton1 = await findByTestId("sa-btn-dl-custom-0");
    fireEvent.click(customButton1);
    expect(button1Click).toBeCalledTimes(1);

    const customButton2 = await findByTestId("sa-btn-dl-custom-1");
    fireEvent.click(customButton2);
    expect(button2Click).toBeCalledTimes(1);
});