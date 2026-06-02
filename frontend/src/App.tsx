import { useState, type ChangeEvent } from "react";
import "./styles/reset.css";
import "./styles/app.css";

interface Note {
  id: number;
  title: string;
  content: string;
  created_at: string;
}

interface User {
  id: number;
  email: string;
  auth_provider_id: string;
}

const mockNotes: Note[] = [
  {
    id: 1,
    title: "React Hooks Guide",
    content:
      "# React Hooks\n\nHooks let you use state and other React features without writing a class.\n\n## useState\nManage component state...",
    created_at: "2024-01-15T10:30:00Z",
  },
  {
    id: 2,
    title: "TypeScript Basics",
    content:
      "# TypeScript Essentials\n\nTypeScript is a typed superset of JavaScript...",
    created_at: "2024-01-14T14:20:00Z",
  },
  {
    id: 3,
    title: "PostgreSQL with pgvector",
    content:
      "# Vector Search in PostgreSQL\n\nUsing pgvector extension for semantic search...",
    created_at: "2024-01-13T09:15:00Z",
  },
];

function App() {
  const [notes, setNotes] = useState(mockNotes);
  const [searchTerm, setSearchTerm] = useState("");
  const [noteTitle, setNoteTitle] = useState("");
  const [isSignedIn, setIsSignedIn] = useState(true);

  const handleSearch = (event: ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(event.currentTarget.value);
  };

  return (
    <>
      <div className="header">
        <h1>Recall IO</h1>
        <button>{isSignedIn ? "Log Out" : "Sign In/Up"}</button>
      </div>
      <div className="main-container">
        <div className="column">
          <h2>Add Note</h2>
          <CustomInput
            inputAttr={{
              value: noteTitle,
              onHandler: handleSearch,
              id: "title",
              type: "text",
              placeholder: "Title your note...",
              label: "Title",
              classname: "note-title",
            }}
            isFocused
          />
          <MarkdownTextArea
            areaAttr={{
              placeholder: "Content... Markdown Supported",
              label: "Content",
              rows: 8,
              cols: 30,
              id: "content",
              classname: "markdown-text-area",
            }}
            isFocused
          />
        </div>
        <div className="column column-scrollable">
          <div className="search-container">
            <CustomInput
              inputAttr={{
                value: searchTerm,
                onHandler: handleSearch,
                id: "search",
                type: "text",
                placeholder: "Search...",
                label: "",
                classname: "search-bar",
              }}
              isFocused
            />
            <button className="search-button">Find</button>
          </div>
          <List list={notes} />
        </div>
      </div>
    </>
  );
}

type TextAreaProps = {
  areaAttr: {
    placeholder: string;
    label: string;
    rows: number;
    cols: number;
    id: string;
    classname: string;
  };
  isFocused: boolean;
};

function MarkdownTextArea({ areaAttr, isFocused }: TextAreaProps) {
  return (
    <>
      <label>{areaAttr.label}</label>
      <textarea
        placeholder={areaAttr.placeholder}
        id={areaAttr.id}
        rows={areaAttr.rows}
        cols={areaAttr.cols}
        className={areaAttr.classname}
        autoFocus={isFocused}
      />
    </>
  );
}

type InputProps = {
  inputAttr: {
    placeholder: string;
    id: string;
    type?: string;
    value: string;
    label: string;
    classname: string;
    onHandler: (event: ChangeEvent<HTMLInputElement>) => void;
  };
  isFocused: boolean;
};

function CustomInput({ inputAttr, isFocused }: InputProps) {
  const handleChange = (event: ChangeEvent<HTMLInputElement>) => {
    inputAttr.onHandler(event);
  };

  return (
    <>
      <label>{inputAttr.label}</label>
      <div className="input-container">
        <input
          placeholder={inputAttr.placeholder}
          id={inputAttr.id}
          type={inputAttr.type || "text"}
          value={inputAttr.value}
          className={inputAttr.classname}
          onChange={handleChange}
          autoFocus={isFocused}
        />
      </div>
    </>
  );
}

type ListProps = {
  list: Note[];
};

function List({ list }: ListProps) {
  return (
    <>
      {list.map((item: Note) => (
        <Item key={item.id} item={item} />
      ))}
    </>
  );
}

type ItemProps = {
  item: Note;
};

function Item({ item }: ItemProps) {
  return (
    <div className="note-item">
      <h3>{item.title}</h3>
      <p>{item.content}</p>
      <span>{item.created_at}</span>
    </div>
  );
}

export default App;
