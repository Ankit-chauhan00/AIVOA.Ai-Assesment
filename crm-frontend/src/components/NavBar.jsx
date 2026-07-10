

const NavBar = () => {
  return (
    <nav className="fixed top-0 h-[72px] flex items-center  bg-assistant-800 w-full z-50">
        <div className="w-full flex px-10 flex-row items-center gap-2  justify-center">
            <div className="font-display text-5xl bg-primary p-1 rounded-md text-clinical-100 ">
                Aivoa.
                <span>AI</span>
            </div>
            <span className="text-clinical-50">(Assignment)</span>
        </div>
    </nav>
  )
}

export default NavBar