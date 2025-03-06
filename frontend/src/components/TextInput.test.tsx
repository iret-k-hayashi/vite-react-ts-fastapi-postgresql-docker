import userEvent from "@testing-library/user-event";
import { render, screen } from "@testing-library/react";
import TextInput from "./TextInput";

test("TextInput Component Test", async () => {
  const user = userEvent.setup();

  render(<TextInput />);
  const textElement = screen.getByText("Entered Text:");
  expect(textElement).toBeInTheDocument();

  const inputElement = screen.getByLabelText("text-input");
  await user.type(inputElement, "Hello, World!");
  expect(inputElement).toHaveValue("Hello, World!");
});
