import Spinner from "@/components/spinner";
import React from "react";

function Loading() {
  return (
    <div className="min-h-screen flex items-center justify-center">
      <Spinner />
    </div>
  );
}

export default Loading;
