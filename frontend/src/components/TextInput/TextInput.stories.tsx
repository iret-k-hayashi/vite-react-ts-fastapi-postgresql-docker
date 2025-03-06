import { Meta, StoryObj } from "@storybook/react";
import TextInput from "./TextInput";

export default {
  title: "TextInput",
  component: TextInput,
  tags: ["autodocs"],
  args: {},
} satisfies Meta<typeof TextInput>;

type Story = StoryObj<typeof TextInput>;

export const Default: Story = {};
