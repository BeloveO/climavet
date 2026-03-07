import { useState, useEffect } from "react";
import { useSelector } from "react-redux";
import { fetchChecklists } from "../services/checklistService";

const useChecklists = (CheckListId) => {
  const [checklists, setChecklists] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const clinicId = useSelector((state) => state.clinic.id);

  useEffect(() => {
    if (CheckListId) {
      fetchChecklists(CheckListId, clinicId)
        .then((data) => {
          setChecklists(data);
          setLoading(false);
        })
        .catch((err) => {
          setError(err.message || "Failed to fetch checklists");
          setLoading(false);
        });
    }
  }, [CheckListId, clinicId]);

  const refreshChecklists = () => {
    setLoading(true);
    fetchChecklists(CheckListId, clinicId)
      .then((data) => {
        setChecklists(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message || "Failed to fetch checklists");
        setLoading(false);
      });
  };

  const addChecklist = (newChecklist) => {
    setChecklists((prev) => [...prev, newChecklist]);
  };

  const updateChecklist = (updatedChecklist) => {
    setChecklists((prev) =>
      prev.map((checklist) =>
        checklist.id === updatedChecklist.id ? updatedChecklist : checklist
      )
    );
  };

  const deleteChecklist = (checklistId) => {
    setChecklists((prev) => prev.filter((checklist) => checklist.id !== checklistId));
  };

  const toggleChecklistItem = (checklistId, itemId) => {
    setChecklists((prev) =>
      prev.map((checklist) => {
        if (checklist.id === checklistId) {
          return {
            ...checklist,
            items: checklist.items.map((item) =>
              item.id === itemId ? { ...item, completed: !item.completed } : item
            ),
          };
        }
        return checklist;
      })
    );
  };

  const exportChecklist = (checklistId) => {
    const checklist = checklists.find((c) => c.id === checklistId);
    if (checklist) {
      const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(checklist));
      const downloadAnchorNode = document.createElement("a");
      downloadAnchorNode.setAttribute("href", dataStr);
      downloadAnchorNode.setAttribute("download", `${checklist.name}.json`);
      document.body.appendChild(downloadAnchorNode);
      downloadAnchorNode.click();
      downloadAnchorNode.remove();
    }
  };


  return { checklists, loading, error, refreshChecklists, addChecklist, updateChecklist, deleteChecklist, toggleChecklistItem, exportChecklist };
};

export default useChecklists;