const MessageInput = () => {
  return (
    <div className="fixed bottom-0 left-0 w-full bg-white shadow-md p-4">
      <textarea
        placeholder="Type your message here..."
        className="w-full h-24 resize-none rounded-lg border border-gray-400 p-3 text-sm
          focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
      />
    </div>
  );
}

export default MessageInput;
