import React from "react";
import { Ring2 } from "ldrs/react";
import "ldrs/react/Ring2.css";

export default function Spinner({
  size = 24,
  ...props
}: React.ComponentProps<typeof Ring2>) {
  return (
    <Ring2
      size={size}
      {...props}
      stroke="5"
      strokeLength="0.25"
      bgOpacity="0.1"
    />
  );
}
