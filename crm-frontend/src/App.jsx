import ChatPannel from "./components/ChatPannel";
import InteractionForm from "./components/InteractionForm";
import NavBar from "./components/NavBar";

const App = () => {
  return (
    <>
      <NavBar/>
      <div className="flex pt-25 gap-5 pb-10 bg-primary pl-5 pr-5 h-screen md:flex-row flex-col">
        <InteractionForm />
        <ChatPannel />
      </div>
    </>
  );
};

export default App;
